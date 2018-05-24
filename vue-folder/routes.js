import AddGood from "./components/AddGood";
import Apothecary from "./components/Apothecary";
import ConfirmingRecipe from "./components/ConfirmingRecipes";
import CreateRecipePage from "./components/CreateRecipePage";
import CreatingWorker from "./components/CreatingWorker";
import LoginPage from "./components/LoginPage";
import PatientRecipe from "./components/PatientRecipe";
import Recipes from "./components/Recipes";
import Workers from "./components/Workers";

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
  new Route("/patient", PatientRecipe),
  new Route("/doctor", CreateRecipePage),
  new Route("/workers/new", CreatingWorker),
  new Route("/workers", Workers),
  new Route("", LoginPage)
];
