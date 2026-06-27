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
import type { SignupResponse } from "~/features/auth/type";

export function SignupRequestPanel() {
  const fetcher = useFetcher<SignupResponse>();
  const isSubmitting = fetcher.state === "submitting";

  return (
    <Card>
      <CardHeader>
        <CardTitle>회원가입 요청</CardTitle>
        <CardDescription>email + password</CardDescription>
      </CardHeader>
      <CardContent>
        <fetcher.Form className="grid gap-4" method="post">
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="signup-email">Email</FieldLabel>
              <Input id="signup-email" name="email" type="email" required />
            </Field>
            <Field>
              <FieldLabel htmlFor="signup-password">Password</FieldLabel>
              <Input
                id="signup-password"
                name="password"
                type="password"
                minLength={8}
                required
              />
              <FieldDescription>8자 이상 입력하세요.</FieldDescription>
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
                  ? "요청 실패"
                  : "요청을 받았습니다"}
              </AlertTitle>
              <AlertDescription>{fetcher.data.message}</AlertDescription>
            </Alert>
          ) : null}

          <div className="flex items-center gap-3">
            <Button
              type="submit"
              disabled={isSubmitting}
              className="cursor-pointer"
            >
              {isSubmitting ? "Sending..." : "Send"}
            </Button>
          </div>
        </fetcher.Form>
      </CardContent>
    </Card>
  );
}
