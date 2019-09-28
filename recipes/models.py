from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from recipes.managers import CustomUserManager


class MedicineType(models.Model):
    type_name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип препората'
        verbose_name_plural = 'Типы препаратов'

    def __str__(self):
        return self.type_name


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        validators=(validators.RegexValidator(r'([^\W\d_]| )+', message='Имя должно содержать только буквы'),)
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        validators=(validators.RegexValidator(r'([^\W\d_]| )+', message='Фамилия должна содержать только буквы'),)
    )
    email = models.EmailField(max_length=150, unique=True, verbose_name='E-mail')
    password = models.CharField(max_length=128, verbose_name='Пароль', validators=(validators.MinLengthValidator(5),))
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='Номер телефона',
        validators=(validators.RegexValidator(r'^\+7\d{10}', message='Должно начинаться с +7 и содержать 11 цифр'),
                    validators.MinLengthValidator(12),
                    validators.MaxLengthValidator(12)))
    is_admin = models.BooleanField(default=False, verbose_name='Админ?')

    username = None

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'password']
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def role(self):
        if hasattr(self, 'doctor'):
            return 'doctor'

        if hasattr(self, 'apothecary'):
            return 'apothecary'

        return ''


class Hospital(models.Model):
    city = models.ForeignKey(City, null=False, on_delete=models.CASCADE, verbose_name='Город')
    hospital_name = models.CharField(max_length=20, verbose_name='Название')

    class Meta:
        verbose_name = 'Больница'
        verbose_name_plural = 'Больницы'

    def __str__(self):
        return self.hospital_name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    hospital = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE, verbose_name='Больница')

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return self.user.email

    def get_initials(self):
        return str(self.user)


class Recipe(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Врач')
    patient_email = models.CharField(max_length=50, verbose_name='E-mail пациента')
    patient_initials = models.CharField(max_length=100, verbose_name='ФИО пациента')
    date = models.DateTimeField(auto_now=True, verbose_name='Выписан')
    token = models.TextField(verbose_name='Идентификатор')
    day_duration = models.PositiveIntegerField(default=15,
                                               verbose_name='Действительность рецепта (в днях)')
    patient_age = models.PositiveSmallIntegerField(verbose_name='Возраст пациента')
    medicine_card_number = models.CharField(max_length=10, null=True, blank=True)
    medicine_policy_number = models.CharField(max_length=16, null=True, blank=True)
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def get_date_str(self):
        return self.date.strftime('%d.%m.%Y')

    def __str__(self):
        return f'{self.date} - {self.patient_email} - {self.doctor.user.email}'

    def get_doctor_initials(self):
        return self.doctor.get_initials()

    def get_doctor_email(self):
        return self.doctor.user.email

    @property
    def requests(self):
        return MedicineRequest.objects.filter(recipe=self)


class Pharmacy(models.Model):
    pharmacy_name = models.CharField(max_length=20, verbose_name='Название')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, verbose_name='Город')
    pharmacy_address = models.TextField(verbose_name='Адрес')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Аптека'
        verbose_name_plural = 'Аптеки'

    def __str__(self):
        return self.pharmacy_name


class Apothecary(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, verbose_name='Аптека')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Аптекарь'
        verbose_name_plural = 'Аптекари'

    def __str__(self):
        return f'{self.user.email} - {self.pharmacy.pharmacy_name}'


class MedicineRequestStatus(models.Model):
    status_name = models.CharField(max_length=20, verbose_name='Название')

    class Meta:
        verbose_name = 'Статус заявки препората'
        verbose_name_plural = 'Статусы заявки препаратов'


class MedicineName(models.Model):
    medicine_name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    medicine_level = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Название препората'
        verbose_name_plural = 'Названия препаратов'

    @property
    def medicine_types(self):
        return MedicineType.objects.filter(medicine__medicine_name_id=self.id)

    def __str__(self):
        return self.medicine_name


class Medicine(models.Model):
    medicine_name = models.ForeignKey(MedicineName, on_delete=models.CASCADE, verbose_name='Название')
    medicine_type = models.ForeignKey(MedicineType, on_delete=models.CASCADE, verbose_name='Тип')
    pharmacies = models.ManyToManyField(Pharmacy, through='Good')

    class Meta:
        verbose_name = 'Препорат'
        verbose_name_plural = 'Препораты'

    def __str__(self):
        return self.medicine_name.medicine_name

    @property
    def name(self):
        return self.medicine_name.medicine_name

    @property
    def type(self):
        return self.medicine_type.type_name


class MedicineDosage(models.Model):
    dosage = models.TextField()
    frequency = models.TextField()
    period = models.TextField()
    medicine = models.ForeignKey(MedicineName, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.medicine.medicine_name} {self.dosage} {self.frequency}'


class MedicineRequest(models.Model):
    medicine_dosage = models.ForeignKey(MedicineDosage, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    medicine_count = models.SmallIntegerField(default=0)
    given_medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, blank=True)
    request_confirmation_time = models.DateTimeField(null=True, blank=True)
    apothecary = models.ForeignKey(Apothecary, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Запрос на лекарство'
        verbose_name_plural = 'Запросы на лекарства'

    @property
    def is_accepted(self):
        return self.medicine_count > 0

    @property
    def medicine_frequency(self):
        return self.medicine_dosage.frequency

    @property
    def dosage(self):
        return self.medicine_dosage.dosage

    @property
    def medicine_period(self):
        return self.medicine_dosage.period

    @property
    def medicine_name(self):
        return self.medicine_dosage.medicine.medicine_name

    @property
    def medicine_name_id(self):
        return self.medicine_dosage.medicine.id


class Good(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name='Лекарство')
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, verbose_name='Аптека')
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.FloatField(default=0.0, validators=(validators.MinValueValidator(0),), verbose_name='Цена')

    class Meta:
        unique_together = ('medicine', 'pharmacy')
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    @property
    def name(self):
        return self.medicine.name

    @property
    def type(self):
        return self.medicine.type

    @property
    def level(self):
        return self.medicine.medicine_name.medicine_level

    def __str__(self):
        return f'{self.medicine} - {self.pharmacy}'
