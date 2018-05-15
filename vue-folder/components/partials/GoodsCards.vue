<template>
  <div>
    <div class="container">
      <search-bar/>
      <div id="goods-cards">
        <new-good-card/>
        <div v-for="medicine in foundMedicines">
          <good-card v-bind:medicine="medicine"></good-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";

  import GoodCard from "./GoodCard";
  import NewGoodCard from "./NewGoodCard";
  import SearchBar from "./SearchBar";

  export default {
    name: "GoodsCards",
    components: {
      GoodCard,
      NewGoodCard,
      SearchBar
    },
    data() {
      return {
        medicines: []
      }
    },
    computed: {
      foundMedicines() {
        if (this.$store.state.searchText === "") {
          return this.medicines;
        } else {
          return this.medicines.filter(medicine => medicine.name.includes(this.$store.state.searchText));
        }
      }
    },
    beforeMount() {
      axios.get("/api/medicines")
        .then(response => this.medicines = response.data)
        .catch(error => this.medicines = []);
    }
  }
</script>

<style lang="less" scoped>
  #goods-cards {
    display: grid;
    margin: 10px auto;
  }

  @media screen and (min-width: 1100px) {
    #goods-cards {
      grid-template-columns: auto auto auto auto auto;
    }
  }

  @media screen and (min-width: 880px) and (max-width: 1099px) {
    #goods-cards {
      grid-template-columns: auto auto auto auto;
    }
  }

  @media screen and (min-width: 660px) and (max-width: 879px) {
    #goods-cards {
      grid-template-columns: auto auto auto;
    }
  }

  @media screen and (min-width: 440px) and (max-width: 659px) {
    #goods-cards {
      grid-template-columns: auto auto;
    }
  }

  #search-block {
    margin: 10px auto;
    text-align: center;
  }

  #search-block #search-input {
    width: 300px;
    height: 30px;
    font-size: 16px;
    border-radius: 10px;
    border: 2px solid #087e8b;
    outline: none;
  }

  #search-block #search-input:focus {
    border-color: #78b8bf;
  }

  #search-block label {
    font-size: 25px;
    font-weight: normal;
  }

  .container {
    margin-top: 20px;

    .form-group {
      text-align: center;
    }
  }
</style>
