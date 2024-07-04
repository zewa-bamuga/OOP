import { stringify } from "query-string";
import { fetchUtils, DataProvider } from "ra-core";

const resourceMapping: Record<string, string> = {
  users: "api/users/v1",
  attachments: "api/storage/v1/attachments",
};

const camelToSnakeCase = (str: string) =>
  str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);

export default (
  apiUrl: string,
  httpClient = fetchUtils.fetchJson
): DataProvider => ({
  getList: (resource, params) => {
    const { page, perPage } = params.pagination;
    const { field, order } = params.sort;
    const query = {
      ...fetchUtils.flattenObject(params.filter),
      sort: camelToSnakeCase(field),
      order: order.toLowerCase(),
      skip: (page - 1) * perPage,
      limit: perPage,
    };
    const url = `${apiUrl}/${resourceMapping[resource]}?${stringify(query)}`;

    return httpClient(url).then(({ headers, json }) => {
      return {
        data: json.items,
        total: json.count,
      };
    });
  },

  getOne: (resource, params) =>
    httpClient(`${apiUrl}/${resourceMapping[resource]}/${params.id}`).then(
      ({ json }) => ({
        data: json,
      })
    ),

  getMany: (resource, params) => {
    if (params.ids.length == 1) {
      const url = `${apiUrl}/${resourceMapping[resource]}/${params.ids[0]}`;
      return httpClient(url).then(({ json }) => ({ data: [json] }));
    }
    const query = {
      id: params.ids,
    };
    const url = `${apiUrl}/${resourceMapping[resource]}?${stringify(query)}`;
    return httpClient(url).then(({ json }) => ({ data: json }));
  },

  getManyReference: (resource, params) => {
    const { page, perPage } = params.pagination;
    const { field, order } = params.sort;
    const query = {
      ...fetchUtils.flattenObject(params.filter),
      [params.target]: params.id,
      _sort: field,
      _order: order,
      _start: (page - 1) * perPage,
      _end: page * perPage,
    };
    const url = `${apiUrl}/${resourceMapping[resource]}?${stringify(query)}`;

    return httpClient(url).then(({ headers, json }) => {
      return {
        data: json.items,
        total: json.count,
      };
    });
  },

  update: (resource, params) =>
    httpClient(`${apiUrl}/${resourceMapping[resource]}/${params.id}`, {
      method: "PATCH",
      body: JSON.stringify(params.data),
    }).then(({ json }) => ({ data: json })),

  // json-server doesn't handle filters on UPDATE route, so we fallback to calling UPDATE n times instead
  updateMany: (resource, params) =>
    Promise.all(
      params.ids.map((id) =>
        httpClient(`${apiUrl}/${resourceMapping[resource]}/${id}`, {
          method: "PUT",
          body: JSON.stringify(params.data),
        })
      )
    ).then((responses) => ({ data: responses.map(({ json }) => json.id) })),

  create: (resource, params) => {
    if (resource === "attachments") {
      let formData = new FormData();
      formData.append("attachment", params.data.attachments.rawFile);

      return httpClient(`${apiUrl}/${resourceMapping[resource]}`, {
        method: "POST",
        body: formData,
      }).then(({ json }) => ({
        data: { ...params.data, id: json.id },
      }));
    }

    return httpClient(`${apiUrl}/${resourceMapping[resource]}`, {
      method: "POST",
      body: JSON.stringify(params.data),
    }).then(({ json }) => ({
      data: { ...params.data, id: json.id },
    }));
  },

  delete: (resource, params) =>
    httpClient(`${apiUrl}/${resourceMapping[resource]}/${params.id}`, {
      method: "DELETE",
    }).then(({ json }) => ({ data: json })),

  // json-server doesn't handle filters on DELETE route, so we fallback to calling DELETE n times instead
  deleteMany: (resource, params) =>
    Promise.all(
      params.ids.map((id) =>
        httpClient(`${apiUrl}/${resourceMapping[resource]}/${id}`, {
          method: "DELETE",
        })
      )
    ).then((responses) => ({ data: responses.map(({ json }) => json.id) })),
});
