import { LandingPage } from "~/features/landing/screens/landing-page";
import type { Route } from "./+types/home";
import {
  getUsersInfo,
  postLoginRequest,
  postSignupRequest,
} from "~/features/auth/api";
import {
  getDatabaseHealthResponse,
  getHealthResponse,
  getWorkerHealthResponse,
} from "~/features/health/api";

export const loader = async () => {
  const [server, database, worker, users] = await Promise.all([
    getHealthResponse(),
    getDatabaseHealthResponse(),
    getWorkerHealthResponse(),
    getUsersInfo(),
  ]);

  return {
    health: { server, database, worker },
    users,
  };
};

export const action = async ({ request }: Route.ActionArgs) => {
  const formData = await request.formData();
  const intent = String(formData.get("intent") ?? "signup");
  const email = String(formData.get("email") ?? "");
  const password = String(formData.get("password") ?? "");

  if (intent === "login") {
    try {
      return await postLoginRequest({ email, password });
    } catch {
      return {
        status: "error" as const,
        email,
        access_token: null,
        message: "로그인 요청에 실패했습니다.",
      };
    }
  }

  if (intent === "signup") {
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
}

export default function Home({ loaderData }: Route.ComponentProps) {
  return <LandingPage homeData={loaderData} />;
}
