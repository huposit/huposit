import { LandingPage } from "~/features/landing/screens/landing-page";
import type { Route } from "./+types/home";
import { postSignupRequest } from "~/features/auth/api";
import {
  getDatabaseHealthResponse,
  getHealthResponse,
  getWorkerHealthResponse,
} from "~/features/health/api";

export const loader = async () => {
  const [server, database, worker] = await Promise.all([
    getHealthResponse(),
    getDatabaseHealthResponse(),
    getWorkerHealthResponse(),
  ]);

  return {
    health: { server, database, worker },
  };
};

export const action = async ({ request }: Route.ActionArgs) => {
  const formData = await request.formData();
  const email = String(formData.get("email") ?? "");
  const password = String(formData.get("password") ?? "");

  try {
    return await postSignupRequest({ email, password });
  } catch {
    return {
      status: "error" as const,
      email,
      email_verified: false,
      message: "회원가입 요청에 실패했습니다.",
    };
  }
};

export default function Home({ loaderData }: Route.ComponentProps) {
  return <LandingPage homeData={loaderData} />;
}
