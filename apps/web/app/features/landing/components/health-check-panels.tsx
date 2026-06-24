import { useRevalidator } from "react-router";
import { Button } from "~/core/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
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
  const revalidator = useRevalidator()
  const isRefreshing = revalidator.state === "loading"

  const { server, database, worker } = health
  const healthCardData = [
    {
      title: "API Health",
      status: server.status,
      content: server.status === "ok" ? "healthy" : "unhealthy",
    },
    {
      title: "DB Connection",
      status: database.status,
      content: database.database,
    },
    {
      title: "Worker",
      status: worker.status,
      content: worker.worker,
    },
  ];

  return (
    <section className="grid gap-4 md:grid-cols-3">
      {healthCardData.map(({ title, status, content }) => (
        <Card key={title}>
          <CardHeader>
            <CardTitle>{title}</CardTitle>
            <CardAction>
              <Button
                type="button"
                onClick={revalidator.revalidate}
                disabled={isRefreshing}
                variant={status === "ok" ? "default" : "destructive"}
                className="cursor-pointer"
              >
                {isRefreshing ? "Checking ..." : "Check"}
              </Button>
            </CardAction>
          </CardHeader>
          <CardContent>
            {content}
          </CardContent>
        </Card>
      ))}
    </section>
  );
}
