import { renderToString } from "react-dom/server";
import { createMemoryRouter, RouterProvider } from "react-router";
import { describe, expect, it } from "vitest";

import { LandingPage } from "./landing-page";
import type { LandingPageProps } from "./landing-page";

describe("LandingPage", () => {
  it("renders health check cards", () => {
    const router = createMemoryRouter([
      {
        path: "/",
        element: <LandingPage homeData={homeData} />,
      },
    ]);

    const html = renderToString(<RouterProvider router={router} />);

    expect(html).toContain("개인 맥락을 저장하고 다시 찾는 작업 공간");
    expect(html).toContain("회원가입 요청");
    expect(html).toContain("가입된 회원");
    expect(html).toContain("person@example.com");
    expect(html).toContain("API Health");
    expect(html).toContain("DB Connection");
    expect(html).toContain("Worker");
  });
});

const homeData: LandingPageProps["homeData"] = {
  health: {
    server: { status: "ok" },
    database: { status: "ok", database: "connected" },
    worker: { status: "ok", worker: "available", mode: "api_placeholder" },
  },
  users: [
    {
      id: "8bf65c82-54b8-4e78-9713-74a3e70bba2f",
      email: "person@example.com",
      email_verified: false,
      created_at: "2026-06-27T05:30:00Z",
    },
  ],
};
