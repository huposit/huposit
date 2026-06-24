export type HealthResponse = {
  status: "ok";
};

export type DatabaseHealthResponse = {
  status: "ok" | "error";
  database: "connected" | "disconnected";
};

export type WorkerHealthResponse = {
  status: "ok";
  worker: "available";
  mode: "api_placeholder";
};
