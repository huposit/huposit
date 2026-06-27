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

export type JsonRequestBody<T> = T extends {
  requestBody: {
    content: {
      "application/json": infer Request;
    };
  };
}
  ? Request
  : never;
