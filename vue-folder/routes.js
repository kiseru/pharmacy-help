import AddGood from "./components/AddGood";
import Apothecary from "./components/Apothecary";
import Doctor from "./components/Doctor";
import HomePage from "./components/HomePage";
import NotFound from "./components/NotFound";

class Route {
    constructor(path, component) {
        this.path = path;
        this.component = component;
    }
}

export default [
  new Route("/apothecary/new", AddGood),
  new Route("/apothecary", Apothecary),
  new Route("/doctor", Doctor),
  new Route("/error", NotFound),
  new Route("/", HomePage)
];
