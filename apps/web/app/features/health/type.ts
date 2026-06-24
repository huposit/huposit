import type { paths } from "~/core/api/openapi-types";
import type { JsonResponse } from "~/core/api/openapi-helpers";

export type HealthResponse = JsonResponse<paths["/health"]["get"]>;
export type DatabaseHealthResponse = JsonResponse<paths["/health/db"]["get"]>;
export type WorkerHealthResponse = JsonResponse<paths["/health/worker"]["get"]>;
