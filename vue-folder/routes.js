import AddGood from "./components/AddGood";
import Apothecary from "./components/Apothecary";
import CreateRecipePage from "./components/CreateRecipePage";
import HomePage from "./components/HomePage";
import PatientRecipe from "./components/PatientRecipe";
import Recipes from "./components/Recipes";

class Route {
    constructor(path, component) {
        this.path = path;
        this.component = component;
    }
}

export default [
  new Route("/apothecary/recipes", Recipes),
  new Route("/apothecary/new", AddGood),
  new Route("/apothecary", Apothecary),
  new Route("/doctor", CreateRecipePage),
  new Route("/patient", PatientRecipe),
  new Route("", HomePage)
];
