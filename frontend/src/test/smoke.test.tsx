import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import App from "../App";

describe("frontend smoke test", () => {
  it("renders the application", () => {
    const { container } = render(<App />);
    expect(container.firstChild).not.toBeNull();
  });

  it("can render again after cleanup", () => {
    const { container } = render(<App />);
    expect(container.firstChild).not.toBeNull();
  });
});