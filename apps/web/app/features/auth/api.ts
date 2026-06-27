import { getApi, postApi } from "~/core/api/client";
import type { SignupRequest, SignupResponse, UsersInfoResponse } from "./type";

export const postSignupRequest = async (
  request: SignupRequest,
): Promise<SignupResponse> => {
  return await postApi<SignupResponse, SignupRequest>(
    "/auth/signup",
    request,
  );
};

export const getUsersInfo = async (): Promise<UsersInfoResponse> => {
  return await getApi<UsersInfoResponse>("/auth/users");
};
