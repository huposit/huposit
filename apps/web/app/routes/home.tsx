import type { Route } from "./+types/home";

export const loader = async () => {
  return { home: "loader" };
};

export const action = async () => {};

export default function Home({ loaderData }: Route.ComponentProps) {
  console.log(loaderData);

  return <h1> hi </h1>;
}
