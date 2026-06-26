import { postApi } from "~/core/api/client";
import type { SignupRequest, SignupResponse } from "./type";

export const postSignupRequest = async (
  request: SignupRequest,
): Promise<SignupResponse> => {
  return await postApi<SignupResponse, SignupRequest>(
    "/auth/signup",
    request,
  );
};
