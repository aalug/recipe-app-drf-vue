import {Tag} from './Tag';
import {Ingredient} from './Ingredient';

export interface Recipe {
  id?: number;
  title: string;
  timeMinutes: number;
  price: string;
  link?: string;
  tags?: Tag[];
  ingredients?: Ingredient[];
  description?: string;
  image?: string | File | null;
}
