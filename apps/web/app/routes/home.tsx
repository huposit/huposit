import { LandingPage } from "~/features/landing/screens/landing-page";
import type { Route } from "./+types/home";
import {
  getDatabaseHealthResponse,
  getHealthResponse,
  getWorkerHealthResponse
} from "~/features/health/api";


export const loader = async () => {

  const [server, database, worker] = await Promise.all([
    getHealthResponse(),
    getDatabaseHealthResponse(),
    getWorkerHealthResponse()
  ])

  return {
    health: { server, database, worker }
  };
};

export default function Home({ loaderData }: Route.ComponentProps) {
  const homeData = loaderData

  return <LandingPage homeData={homeData} />;
}
