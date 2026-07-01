import { useFetcher } from "react-router";

import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "~/core/components/ui/alert";
import { Button } from "~/core/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/core/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "~/core/components/ui/field";
import { Input } from "~/core/components/ui/input";
import type { LoginResponse } from "~/features/auth/type";

export function LoginRequestPanel() {
  const fetcher = useFetcher<LoginResponse>();
  const isSubmitting = fetcher.state === "submitting";
  const tokenPreview = fetcher.data?.access_token
    ? `${fetcher.data.access_token.slice(0, 18)}...`
    : null;

  return (
    <Card>
      <CardHeader>
        <CardTitle>로그인 요청</CardTitle>
        <CardDescription>access token 발급 확인</CardDescription>
      </CardHeader>
      <CardContent>
        <fetcher.Form className="grid gap-4" method="post">
          <input name="intent" type="hidden" value="login" />
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="login-email">Email</FieldLabel>
              <Input id="login-email" name="email" type="email" required />
            </Field>
            <Field>
              <FieldLabel htmlFor="login-password">Password</FieldLabel>
              <Input
                id="login-password"
                name="password"
                type="password"
                minLength={8}
                required
              />
              <FieldDescription>
                가입한 email과 password로 access token 발급을 확인합니다.
              </FieldDescription>
            </Field>
          </FieldGroup>

          {fetcher.data ? (
            <Alert
              variant={
                fetcher.data.status === "error" ? "destructive" : "default"
              }
            >
              <AlertTitle>
                {fetcher.data.status === "error"
                  ? "로그인 실패"
                  : "로그인 성공"}
              </AlertTitle>
              <AlertDescription>
                {fetcher.data.message}
                {tokenPreview ? (
                  <span className="mt-1 block font-mono text-[11px]">
                    token: {tokenPreview}
                  </span>
                ) : null}
              </AlertDescription>
            </Alert>
          ) : null}

          <div className="flex items-center gap-3">
            <Button
              type="submit"
              disabled={isSubmitting}
              className="cursor-pointer"
            >
              {isSubmitting ? "Signing in..." : "Sign in"}
            </Button>
          </div>
        </fetcher.Form>
      </CardContent>
    </Card>
  );
}
