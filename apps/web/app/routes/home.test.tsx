import { renderToString } from "react-dom/server";
import { describe, expect, it } from "vitest";

import Home, { meta } from "./home";
import { Welcome } from "../welcome/welcome";

describe("Home route", () => {
  it("defines default metadata", () => {
    expect(meta()).toEqual([
      { title: "New React Router App" },
      { name: "description", content: "Welcome to React Router!" },
    ]);
  });

  it("exposes the route component", () => {
    expect(Home).toBeTypeOf("function");
  });

  it("renders the welcome screen", () => {
    const html = renderToString(<Welcome />);

    expect(html).toContain("React Router Docs");
  });
});
