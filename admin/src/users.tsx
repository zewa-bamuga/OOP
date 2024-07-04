import {
  TextInput,
  ImageField,
  Datagrid,
  SelectInput,
  ReferenceInput,
  DateField,
  List,
  ArrayInput,
  SimpleFormIterator,
  Create,
  Edit,
  SimpleForm,
  TextField,
  Show,
  SimpleShowLayout,
} from "react-admin";

export const UserList = () => (
  <List sort={{ field: "createdAt", order: "desc" }}>
    <Datagrid rowClick="show">
      <TextField source="username" />
      <TextField source="id" />
      <TextField source="status" />
      <DateField source="createdAt" showTime />
    </Datagrid>
  </List>
);

export const UserShow = () => {
  return (
    <Show>
      <SimpleShowLayout>
        <TextField source="id" />
        <TextField source="username" />
        <TextField source="status" />
        <ImageField
          source="avatarAttachment.uri"
          title="avatarAttachment.name"
          label="Avatar"
        />
        <DateField source="createdAt" showTime />
      </SimpleShowLayout>
    </Show>
  );
};

export const UserCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="firstname" />
      <TextInput source="lastname" />
      <TextInput source="email" />
      <TextInput source="password" />
    </SimpleForm>
  </Create>
);

export const UserUpdate = () => (
  <Edit>
    <SimpleForm>
      <TextInput source="username" />
      <ArrayInput source="permissions">
        <SimpleFormIterator>
          <TextInput source="fieldName" />
        </SimpleFormIterator>
      </ArrayInput>
      <ReferenceInput
        label="Avatar Attachment"
        source="avatarAttachmentId"
        reference="attachments"
        sort={{ field: "created_at", order: "desc" }}
      >
        <SelectInput optionText="name" />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);

