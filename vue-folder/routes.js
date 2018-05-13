import AddGood from "./components/AddGood";
import Apothecary from "./components/Apothecary";
import ConfirmingRecipe from "./components/ConfirmingRecipes";
import CreateRecipePage from "./components/CreateRecipePage";
import CreatingWorker from "./components/CreatingWorker";
import HomePage from "./components/HomePage";
import PatientRecipe from "./components/PatientRecipe";
import Recipes from "./components/Recipes";
import Workers from "./components/Workers";
import ChangeGoodInfo from "./components/ChangeGoodInfo"

class Route {
    constructor(path, component) {
        this.path = path;
        this.component = component;
    }
}

export default [
  new Route("/apothecary/recipes", Recipes),
  new Route("/apothecary/recipes/:id", ConfirmingRecipe),
  new Route("/apothecary/new", AddGood),
  new Route("/apothecary/:id", ChangeGoodInfo),
  new Route("/apothecary", Apothecary),
  new Route("/patient", PatientRecipe),
  new Route("/doctor", CreateRecipePage),
  new Route("/moderator/new", CreatingWorker),
  new Route("/moderator", Workers),
  new Route("", HomePage)
];
