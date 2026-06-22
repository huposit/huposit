import { renderToString } from "react-dom/server";
import { createMemoryRouter, RouterProvider } from "react-router";
import { describe, expect, it } from "vitest";

import { LandingPage } from "./landing-page";
import type { HealthCheck } from "~/features/health/type";

describe("LandingPage", () => {
  it("renders health check cards", () => {
    const router = createMemoryRouter([
      {
        path: "/",
        element: <LandingPage checks={checks} />,
      },
    ]);

    const html = renderToString(<RouterProvider router={router} />);

    expect(html).toContain("개인 맥락을 저장하고 다시 찾는 작업 공간");
    expect(html).toContain("API Health");
    expect(html).toContain("DB Connection");
    expect(html).toContain("Worker");
  });
});

const checks: HealthCheck[] = [
  {
    id: "health",
    title: "API Health",
    ok: true,
    detail: "status=ok",
    checkedAt: "2026. 6. 22. 오전 9:00:00",
  },
  {
    id: "database",
    title: "DB Connection",
    ok: true,
    detail: "status=ok, database=connected",
    checkedAt: "2026. 6. 22. 오전 9:00:00",
  },
  {
    id: "worker",
    title: "Worker",
    ok: true,
    detail: "worker=available, mode=api_placeholder",
    checkedAt: "2026. 6. 22. 오전 9:00:00",
  },
];
