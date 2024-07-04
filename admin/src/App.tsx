import { fetchUtils, Admin, Resource } from "react-admin";
import provider from "./dataProvider";
import authProvider from "./authProvider";
import { UserList, UserCreate, UserUpdate, UserShow } from "./users";
import {
  AttachmentList,
  AttachmentCreate,
  AttachmentShow,
} from "./attachments";

import UserIcon from "@mui/icons-material/Person";
import AttachmentIcon from "@mui/icons-material/Attachment";

const httpClient = (url: string, options: any = {}) => {
  if (!options.headers) {
    options.headers = new Headers({ Accept: "application/json" });
  }
  const tokenDataString = localStorage.getItem("tokenData");
  if (tokenDataString) {
    const tokenData = JSON.parse(tokenDataString);
    options.headers.set("Authorization", `Bearer ${tokenData.accessToken}`);
  }
  return fetchUtils.fetchJson(url, options);
};

const dataProvider = provider(import.meta.env.VITE_BACKEND_URI, httpClient);

const App = () => (
  <Admin
    dataProvider={dataProvider}
    authProvider={authProvider}
    disableTelemetry
  >
    <Resource
      name="users"
      list={UserList}
      create={UserCreate}
      edit={UserUpdate}
      show={UserShow}
      recordRepresentation="name"
      icon={UserIcon}
    />
    <Resource
      name="attachments"
      list={AttachmentList}
      show={AttachmentShow}
      recordRepresentation="name"
      create={AttachmentCreate}
      icon={AttachmentIcon}
    />
  </Admin>
);

export default App;
