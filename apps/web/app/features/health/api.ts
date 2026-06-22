import { getApi } from "~/core/lib/api-fetch";
import {
  type HealthResponse,
  type DatabaseHealthResponse,
  type WorkerHealthResponse
} from "./type";

export const getHealthResponse = async (): Promise<HealthResponse> => {
  return await getApi<HealthResponse>("/health")
}

export const getDatabaseHealthResponse = async (): Promise<DatabaseHealthResponse> => {
  return await getApi<DatabaseHealthResponse>("/health/db")
}

export const getWorkerHealthResponse = async (): Promise<WorkerHealthResponse> => {
  return await getApi<WorkerHealthResponse>("/health/worker")
}