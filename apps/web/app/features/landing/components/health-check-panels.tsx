import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/core/components/ui/card";

import type {
  DatabaseHealthResponse,
  HealthResponse,
  WorkerHealthResponse,
} from "~/features/health/type";

type HealthCheckPanelsProps = {
  health: {
    server: HealthResponse;
    database: DatabaseHealthResponse;
    worker: WorkerHealthResponse;
  };
};

export function HealthCheckPanels({ health }: HealthCheckPanelsProps) {
  const serverOk = health.server.status === "ok";
  const databaseOk =
    health.database.status === "ok" &&
    health.database.database === "connected";
  const workerOk =
    health.worker.status === "ok" && health.worker.worker === "available";

  return (
    <section className="grid gap-4 md:grid-cols-3">
      <Card size="sm">
        <CardHeader>
          <CardTitle>API Health</CardTitle>
          <CardDescription>API server response</CardDescription>
          <CardAction>
            <span className={serverOk ? "text-primary" : "text-destructive"}>
              {serverOk ? "OK" : "Error"}
            </span>
          </CardAction>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            status={health.server.status}
          </p>
        </CardContent>
      </Card>

      <Card size="sm">
        <CardHeader>
          <CardTitle>DB Connection</CardTitle>
          <CardDescription>Database connection response</CardDescription>
          <CardAction>
            <span className={databaseOk ? "text-primary" : "text-destructive"}>
              {databaseOk ? "OK" : "Error"}
            </span>
          </CardAction>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            status={health.database.status}, database={health.database.database}
          </p>
        </CardContent>
      </Card>

      <Card size="sm">
        <CardHeader>
          <CardTitle>Worker</CardTitle>
          <CardDescription>Worker status response</CardDescription>
          <CardAction>
            <span className={workerOk ? "text-primary" : "text-destructive"}>
              {workerOk ? "OK" : "Error"}
            </span>
          </CardAction>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            status={health.worker.status}, worker={health.worker.worker},
            mode={health.worker.mode}
          </p>
        </CardContent>
      </Card>
    </section>
  );
}
