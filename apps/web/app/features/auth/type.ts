import type { paths } from "~/core/api/openapi-types";
import type {
  JsonRequestBody,
  JsonResponse,
} from "~/core/api/openapi-helpers";

export type SignupRequest = JsonRequestBody<paths["/auth/signup"]["post"]>;
export type SignupResponse = JsonResponse<paths["/auth/signup"]["post"]>;
export type UsersInfoResponse = JsonResponse<paths["/auth/users"]["get"]>;
export type LoginRequest = JsonRequestBody<paths["/auth/login"]["post"]>;
export type LoginResponse = JsonResponse<paths["/auth/login"]["post"]>;
