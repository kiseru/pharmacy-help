import AddGood from "./components/AddGood";
import Apothecary from "./components/Apothecary";
import ConfirmingRecipe from "./components/ConfirmingRecipes";
import CreateRecipePage from "./components/CreateRecipePage";
import Doctor from "./components/Doctor";
import HomePage from "./components/HomePage";
import NotFound from "./components/NotFound";
import PatientRecipe from "./components/PatientRecipe";
import PatientRecipes from "./components/PatientRecipes";
import Recipes from "./components/Recipes";

class Route {
    constructor(path, component) {
        this.path = path;
        this.component = component;
    }
}

export default [
  new Route("/apothecary/recipes", Recipes),
  new Route("/apothecary/recipe", ConfirmingRecipe),
  new Route("/apothecary/new", AddGood),
  new Route("/apothecary", Apothecary),
  new Route("/doctor", Doctor),
  new Route("/error", NotFound),
  new Route("/patient/recipe", PatientRecipe),
  new Route("/patient/recipes", PatientRecipes),
  new Route("/recipe/new", CreateRecipePage),
  new Route("", HomePage)
];
