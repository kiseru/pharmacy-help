<template>
  <apothecary-header v-if="isUserApothecary"/>
  <doctor-header v-else-if="isUserDoctor"/>
</template>

<script>
  import axios from "axios";

  import ApothecaryHeader from "./ApothecaryHeader";
  import DoctorHeader from "./DoctorHeader";

  export default {
    name: "DefaultHeader",
    components: {
      ApothecaryHeader,
      DoctorHeader
    },
    data() {
      return {
        isUserDoctor: false,
        isUserApothecary: false
      };
    },
    beforeMount() {
      axios.get("/api/user")
        .then(response => {
          if (response.data.role === "doctor") this.isUserDoctor = true;
          else if (response.data.role === "apothecary") this.isUserApothecary = true; 
        });
    },
    computed: {
      
    }
  }
</script>

<style lang="less">
</style>
