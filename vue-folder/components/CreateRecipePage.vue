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
            <td>{{ medicine.name }}</td>
            <td>{{ medicine.dosage }}</td>
            <td>{{ medicine.frequency }}</td>
            <td>{{ medicine.period }}</td>
            <td><button class="btn btn-danger">Удалить</button></td>
          </tr>
          <tr>
            <td>
              <input type="text" class="form-control" v-model="newMedicine.name" list="medicines">
              <datalist id="medicines">
                <option v-for="option in options" v-bind:value="option.medicine_name"></option>
              </datalist>
            </td>
            <td><input type="text" class="form-control" v-model="newMedicine.dosage"></td>
            <td><input type="text" class="form-control" v-model="newMedicine.frequency"></td>
            <td><input type="text" class="form-control" v-model="newMedicine.period"></td>
          </tr>
        </tbody>
      </table>

      <button type="button" class="btn btn-primary" v-on:click="createNewMedicine">Добавить препарат</button>

      <hr>

      <button type="button" class="btn btn-success" v-on:click="createRecipe">Создать рецепт</button>
    </div>
  </div>
</template>

<script>
  import axios from "axios";

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
          medicine_id: 0,
          name: "",
          dosage: "",
          frequency: "",
          period: ""
        },
        options: []
      }
    },
    methods: {
      createNewMedicine() {
        if (this.newMedicine.name === "") return;
        if (this.newMedicine.dosage === "") return;
        if (this.newMedicine.frequency === "") return;
        if (this.newMedicine.period === "") return;
        this.newMedicine.medicine_id = this.options[0].id;
        this.patient.medicines.push(this.newMedicine);
        this.newMedicine = {
          medicine_id: 0,
          name: "",
          dosage: "",
          frequency: "",
          period: ""
        };
      },
      createRecipe() {
        if (this.patient.confirmationPeriod < 1) return;
        this.patient.medicines.forEach(medicine => delete medicine.name);
        axios.post("/api/recipes/new", {
            patient_initials: this.patient.name,
            patient_email: this.patient.email,
            medicine_policy_number: this.patient.policeNumber,
            medicine_card_number: this.patient.cardNumber,
            patient_age: this.patient.age,
            day_duration: this.patient.confirmationPeriod,
            medicines: this.patient.medicines
          },
          { headers: { "X-CSRFTOKEN": this.$cookies.get("csrftoken") } })
          .then(response => {
            this.patient = {
              age: "",
              cardNumber: "",
              confirmationPeriod: -1,
              email: "",
              medicines: [],
              name: "",
              policeNumber: ""
            };
            this.newMedicine = {
              medicine_id: 0,
              name: "",
              dosage: "",
              frequency: "",
              period: ""
            };
            this.options = [];
          });
      }
    },
    watch: {
      "newMedicine.name"(newValue, oldValue) {
        axios.get("/api/search/medicine?medicine_name=" + newValue)
          .then(response => this.options = response.data);
      }
    }
  }
</script>

<style lang="less" scoped>
  .create-recipe-form {
    border: 2px solid #087e8b;
    width: 850px;
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

      tr .form-control {
        font-size: 12px;
      }
    }
  }
</style>
