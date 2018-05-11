<template>
  <div class="row justify-content-center">
    <div class="col-4  form-group">
      <label for="search-input">Найти</label><br/>
      <input type="text" id="search-input" class="form-control" v-model="searchText">
      <!--{{ this.$store.state.searchText }}-->
    </div>
  </div>
</template>

<script>
  export default {
    name: 'SearchBar',
    props: {
      searchObj: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        searchText: ""
      }
    },
    watch: {
      searchText(newSearchText, oldSearchText) {
        this.$store.commit("changeSearchText", newSearchText);
      }
    }
  }
</script>
<style lang="less" scoped>

  @media screen and (min-width: 1100px) {
  }

  @media screen and (min-width: 880px) and (max-width: 1099px) {
  }

  @media screen and (min-width: 660px) and (max-width: 879px) {
  }

  @media screen and (min-width: 440px) and (max-width: 659px) {
  }

  .align-self-center {
    text-align: center;

    label {
      font-size: 23px;
      font-weight: normal;
    }
  }

</style>
