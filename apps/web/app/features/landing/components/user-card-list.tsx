import type { UsersInfoResponse } from "~/features/auth/type";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/core/components/ui/card";

export function UserCardList({ users }: { users: UsersInfoResponse }) {
  return (
    <section className="space-y-3">
      <div className="flex items-end justify-between gap-4">
        <div className="space-y-1">
          <h2 className="text-sm font-medium">가입된 회원</h2>
          <p className="text-xs/relaxed text-muted-foreground">
            최근 생성된 계정을 확인합니다.
          </p>
        </div>
        <p className="text-xs text-muted-foreground">{users.length} users</p>
      </div>

      {users.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2">
          {users.map((user) => (
            <Card key={user.id} size="sm">
              <CardHeader>
                <CardTitle className="truncate">{user.email}</CardTitle>
                <CardDescription>
                  {formatCreatedAt(user.created_at)}
                </CardDescription>
              </CardHeader>
              <CardContent className="grid gap-2">
                <div className="flex items-center justify-between gap-3">
                  <span className="text-muted-foreground">이메일 인증</span>
                  <span>{user.email_verified ? "완료" : "대기"}</span>
                </div>
                <p className="break-all text-muted-foreground">{user.id}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="border border-dashed border-border px-4 py-8 text-center text-xs text-muted-foreground">
          아직 가입된 회원이 없습니다.
        </div>
      )}
    </section>
  );
}

function formatCreatedAt(createdAt: string) {
  return new Intl.DateTimeFormat("ko-KR", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(createdAt));
}
