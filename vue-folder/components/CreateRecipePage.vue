<template>
  <div>
    <doctor-header/>
    <div class="create-recipe-form">
      <h4>Создать рецепт</h4>

      <hr>

      <div class="form-group">
        <label for="patientNameInput">ФИО пациента</label>
        <input type="text" class="form-control" id="patientNameInput" v-model="patient.name">
      </div>

      <div>
        <label for="patientEmailInput">E-mail пациента</label>
        <input type="text" class="form-control" id="patientEmailInput" v-model="patient.email">
      </div>

      <div>
        <label for="patientPoliceNumberInput">Номер полиса</label>
        <input type="text" class="form-control" id="patientPoliceNumberInput" v-model="patient.policeNumber">
      </div>

      <div>
        <label for="patientMedCardInput">Номер мед карты</label>
        <input type="text" class="form-control" id="patientMedCardInput" v-model="patient.cardNumber">
      </div>

      <div>
        <label for="patientAgeInput">Возраст</label>
        <input type="number" class="form-control" id="patientAgeInput" v-model="patient.age">
      </div>

      <div>
        <label for="patientСonfirmationPeriodInput">Срок действия</label>
        <input type="number" class="form-control" id="patientСonfirmationPeriodInput" v-model="patient.confirmationPeriod">
      </div>

      <hr>

      <h4>Выписываемые препараты</h4>
      <br>

      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Название</th>
            <th scope="col">Доза</th>
            <th scope="col">Частота</th>
            <th scope="col">Протяженность</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="medicine in patient.medicines">
            <td>{{medicine.name}}</td>
            <td>{{medicine.dosage}}</td>
            <td>{{medicine.frequency}}</td>
            <td>{{medicine.duration}}</td>
          </tr>
        </tbody>
      </table>

      <hr>

      <div>
        <label for="newMedicineNameInput">Название препарата</label>
        <input type="text" class="form-control" id="newMedicineNameInput" v-model="newMedicine.name">
      </div>

      <div>
        <label for="newMedicineDosageInput">Доза</label>
        <input type="text" class="form-control" id="newMedicineDosageInput" v-model="newMedicine.dosage">
      </div>

      <div>
        <label for="newMedicineFrequencyInput">Частота</label>
        <input type="text" class="form-control" id="newMedicineFrequencyInput" v-model="newMedicine.frequency">
      </div>

      <div>
        <label for="newMedicineDurationInput">Протяженность</label>
        <input type="text" class="form-control" id="newMedicineDurationInput" v-model="newMedicine.duration">
      </div>

      <button type="button" class="btn btn-primary" v-on:click="createNewMedicine">Добавить препарат</button>

      <hr>

      <button type="button" class="btn btn-success" v-on:click="createRecipe">Создать рецепт</button>
    </div>
  </div>
</template>

<script>
  import AppInput from "./partials/AppInput";
  import DoctorHeader from "./header/DoctorHeader";

  export default {
    name: "CreateRecipePage",
    components: {
      AppInput,
      DoctorHeader
    },
    data() {
      return {
        patient: {
          age: "",
          cardNumber: "",
          confirmationPeriod: -1,
          email: "",
          medicines: [],
          name: "",
          policeNumber: ""
        },
        newMedicine: {
          name: "",
          dosage: "",
          frequency: "",
          duration: ""
        }
      }
    },
    methods: {
      createNewMedicine() {
        this.patient.medicines.push(this.newMedicine);
        this.newMedicine = {
          name: "",
          dosage: "",
          frequency: "",
          duration: ""
        };
      },
      createRecipe() {

      }
    }
  }
</script>

<style lang="less" scoped>
  .create-recipe-form {
    border: 2px solid #087e8b;
    width: 550px;
    height: auto;
    margin: 20px auto;
    border-radius: 10px;
    background-color: #fff;
    text-align: center;
    padding: 20px;

    hr {
      color: #087e8b;
      background-color: #087e8b;
      border: none;
      height: 1px;
    }

    button {
      margin-top: 20px;
    }

    table {
      margin: 0 auto;
      text-align: center;

      th {
        text-align: center;
      }
    }
  }
</style>
