import {
  Datagrid,
  UrlField,
  ReferenceInput,
  SimpleShowLayout,
  Show,
  FileInput,
  FileField,
  DateField,
  List,
  Create,
  SimpleForm,
  TextField,
} from "react-admin";

export const AttachmentList = () => (
  <List sort={{ field: "createdAt", order: "desc" }}>
    <Datagrid rowClick="show">
      <TextField source="name" />
      <TextField source="id" />
      <UrlField source="uri" />
      <DateField source="createdAt" showTime />
    </Datagrid>
  </List>
);

export const AttachmentShow = () => (
  <Show>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="name" />
      <UrlField source="uri" />
      <DateField source="createdAt" showTime />
    </SimpleShowLayout>
  </Show>
);

export const AttachmentCreate = () => (
  <Create>
    <SimpleForm>
      <FileInput source="attachments">
        <FileField source="src" title="title" />
      </FileInput>
    </SimpleForm>
  </Create>
);
