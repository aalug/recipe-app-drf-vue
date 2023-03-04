export interface Recipe {
  title: string;
  timeMinutes: number;
  price: string;
  link?: string;
  tags?: { name: string }[];
  ingredients?: { name: string }[];
  description?: string;
  image?: File | null;
}
