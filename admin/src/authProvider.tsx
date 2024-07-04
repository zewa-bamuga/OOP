const backendUrl = import.meta.env.VITE_BACKEND_URI;

interface LoginParams {
  firstname: string;
  lastname: string;
  email: string;
  password: string;
}

const authProvider = {
  login: ({ firstname, lastname, email, password }: LoginParams) => {
    const request = new Request(`${backendUrl}/api/users/v1/authentication`, {
      method: "POST",
      body: JSON.stringify({ firstname, lastname, email, password }),
      headers: new Headers({ "Content-Type": "application/json" }),
    });
    return fetch(request)
      .then((response) => {
        if (response.status < 200 || response.status >= 300) {
          throw new Error(response.statusText);
        }
        return response.json();
      })
      .then((auth) => {
        localStorage.setItem("tokenData", JSON.stringify(auth));
      })
      .catch(() => {
        throw new Error("Network error");
      });
  },
  logout: () => {
    localStorage.removeItem("tokenData");
    return Promise.resolve();
  },
  checkAuth: () =>
    localStorage.getItem("tokenData") ? Promise.resolve() : Promise.reject(),
  checkError: (error: { status: number }) => {
    const status = error.status;
    if (status === 401 || status === 403) {
      localStorage.removeItem("tokenData");
      return Promise.reject();
    }
    return Promise.resolve();
  },
  getIdentity: () => {
    try {
      const { id, fullName, avatar } = JSON.parse(
        localStorage.getItem("tokenData") || '{}'
      );
      return Promise.resolve({ id, fullName, avatar });
    } catch (error) {
      return Promise.reject(error);
    }
  },
  getPermissions: () => Promise.resolve(""),
};

export default authProvider;
