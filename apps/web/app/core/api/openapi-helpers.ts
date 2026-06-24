export type JsonResponse<T> = T extends {
  responses: {
    200: {
      content: {
        "application/json": infer Response;
      };
    };
  };
}
  ? Response
  : never;
