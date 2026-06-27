import { HealthCheckPanels } from "../components/health-check-panels";
import { SignupRequestPanel } from "../components/signup-request-panel";
import { UserCardList } from "../components/user-card-list";
import { WhatIsHuposit } from "../components/what-is-huposit";

import type { UsersInfoResponse } from "~/features/auth/type";
import type {
  DatabaseHealthResponse,
  HealthResponse,
  WorkerHealthResponse,
} from "~/features/health/type";

export type LandingPageProps = {
  homeData: {
    health: {
      server: HealthResponse;
      database: DatabaseHealthResponse;
      worker: WorkerHealthResponse;
    };
    users: UsersInfoResponse;
  };
};

export function LandingPage({ homeData }: LandingPageProps) {
  return (
    <main className="min-h-screen bg-background px-6 py-10 text-foreground">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
        <WhatIsHuposit />
        <SignupRequestPanel />
        <UserCardList users={homeData.users} />
        <HealthCheckPanels health={homeData.health} />
      </div>
    </main>
  );
}
