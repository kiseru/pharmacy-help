<template>
  <div>
    <doctor-header/>
    <div class="create-recipe-form mx-auto my-4 rounded bg-white p-4 border border-light">
      <h4 class="border-bottom pb-2 mb-3">Создать рецепт</h4>

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

      <h4 class="border-top p-2 mt-4 mb-0">Выписываемые препараты</h4>

      <table class="table mx-auto mb-0">
        <thead class="thead-light">
          <tr>
            <th scope="col">Название</th>
            <th scope="col">Доза</th>
            <th scope="col">Частота</th>
            <th scope="col">Протяженность</th>
            <th scope="col">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="medicine in patient.medicines">
            <td class="align-middle p-1">{{ medicine.name }}</td>
            <td class="align-middle p-1">{{ medicine.dosage }}</td>
            <td class="align-middle p-1">{{ medicine.frequency }}</td>
            <td class="align-middle p-1">{{ medicine.period }}</td>
            <td class="align-middle p-1">
              <button class="material-icons bg-danger border-0 rounded text-light p-1 mx-1">
                delete_forever
              </button>
            </td>
          </tr>
          <tr>
            <td>
              <input type="text" class="form-control h-75" v-model="newMedicine.name" list="medicines">
              <datalist id="medicines">
                <option v-for="option in options" v-bind:value="option.medicine_name"></option>
              </datalist>
            </td>
            <td><input type="text" class="form-control h-75" v-model="newMedicine.dosage"></td>
            <td><input type="text" class="form-control h-75" v-model="newMedicine.frequency"></td>
            <td><input type="text" class="form-control h-75" v-model="newMedicine.period"></td>
            <td></td>
          </tr>
        </tbody>
      </table>

      <button type="button" class="btn btn-primary mt-2" v-on:click="createNewMedicine">Добавить препарат</button>

      <div class="border-top my-3"></div>

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
    width: 850px;

    hr {
      height: 1px;
    }

    table {

      tr .form-control {
        font-size: 12px;
      }
    }
  }
</style>
