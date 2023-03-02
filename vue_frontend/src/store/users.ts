import {ref} from 'vue';
import {defineStore} from 'pinia';
import axios from 'axios';
import {User} from '@/types/User'
import {validateEmail} from '@/utils/validate-email';

export const useUserStore = defineStore('users', () => {
    const user = ref<User>(new User());
    const token = ref<string | null>(localStorage.getItem('token'));
    const errorMessage = ref<string>('');
    const loading = ref<boolean>(false);
    const isSuccessful = ref<boolean>(false);

    const handleRegister = async (email: string,
                                  name: string,
                                  password: string) => {
      /**
       * Handle the registration of a new user.
       * First, validate the data, then make post request to the server.
       * If there is an error, set the value of errorMessage to the received error message
       */

      if (!validateEmail(email)) {
        return errorMessage.value = 'E-mail is invalid';
      }

      if (!name) {
        return errorMessage.value = 'Name is required';
      }

      if (password.length < 6) {
        return errorMessage.value = 'Password must be at least 6 characters';
      }

      errorMessage.value = '';

      loading.value = true;
      try {
        await axios.post(
          `${import.meta.env.VITE_API_BASE}/user/create/`,
          {
            email: email,
            password: password,
            name: name
          }
        );
        // Registration was successful, set the value appropriately
        isSuccessful.value = true;

        // Clear the error message
        errorMessage.value = '';
      } catch (e) {
        // @ts-ignore
        if (e.response.status === 400) {
          // @ts-ignore
          const errorData = e.response.data;
          const message = ref<string>('');
          if (errorData.email && errorData.name) {
            message.value = 'User with this email and name already exists';
          } else if (errorData.email) {
            message.value = errorData.email[0];
          } else if (errorData.name) {
            message.value = errorData.name[0];
          }
          errorMessage.value = message.value ? message.value : 'Error occurred while creating an account';
        } else {
          errorMessage.value = 'Error occurred while creating an account';
        }
      } finally {
        loading.value = false;
      }
    }

    const handleLogin = async (email: string, password: string) => {
      /**
       * Handle logging-in by getting the auth token
       * fo the given credentials.
       * First, validate the given credentials then make post request,
       * and save the received token.
       */

      // Validation
      if (!validateEmail(email)) return errorMessage.value = 'E-mail is invalid';
      if (password.length < 6) {
        return errorMessage.value = 'Password must be at least 6 characters';
      }

      loading.value = true;
      try {
        const {data} = await axios.post(
          `${import.meta.env.VITE_API_BASE}/user/token/`,
          {
            email: email,
            password: password
          }
        );
        // Store the token in the localStorage
        localStorage.setItem('token', data.token);
        token.value = data.token;

        // Login was successful, set the value appropriately
        isSuccessful.value = true;

        // Clear the error message
        errorMessage.value = '';
      } catch (e) {
        // @ts-ignore
        if (e.response.status === 400) {
          // @ts-ignore
          const errorData = e.response.data;
          const message = ref<string>('');
          if (errorData.nonFieldErrors) {
            message.value = errorData.nonFieldErrors[0];
          }
          errorMessage.value = message.value ? message.value : 'Error occurred while creating an account';
        } else {
          errorMessage.value = 'Error occurred while logging in';
        }
      } finally {
        loading.value = false;
      }
    }

    const getUserInfo = async () => {
      /**
       * Get user information and update the user.value.
       */
      loading.value = true;
      try {
        await axios.get(
          `${import.meta.env.VITE_API_BASE}/user/me/`,
          {headers: {Authorization: `Token ${token.value}`}}
        )
          .then(response => {
              user.value.name = response.data.name;
              user.value.email = response.data.email;
            }
          )
      } catch (e) {
        console.error(e);
      } finally {
        loading.value = false;
      }
    }

    const updateUserProfile = async (email: string, name: string, password: string) => {
      /**
       * Handle updating user's profile information.
       * Based on passed arguments, send put or patch request to the server.
       */
      // Validation
      if (!validateEmail(email)) return errorMessage.value = 'E-mail is invalid'
      if (!name) return errorMessage.value = 'Name is required'
      // If there is a password, but it is less than 6 characters
      if (password && password.length < 6) return errorMessage.value = 'Password must be at least 6 characters'

      const url = `${import.meta.env.VITE_API_BASE}/user/me/`;
      const authHeaders = {headers: {Authorization: `Token ${token.value}`}};

      // If all three arguments are different from the original user's details.
      // (or if password is given - we don't have ability to see the password, only to set the new one)
      if (
        email !== user.value.email &&
        name !== user.value.name &&
        password) {

        loading.value = true;
        try {
          await axios.put(
            url,
            {
              email: email,
              name: name,
              password: password
            },
            authHeaders
          ) // then, update the user info
            .then(async () => {
              await getUserInfo();
              isSuccessful.value = true;
            })
        } catch (e) {
          console.error(e);
          // @ts-ignore
          errorMessage.value = e.message;
        } finally {
          loading.value = false;
        }
      } else {
        // If this `else` is executed, that means that less than three
        // arguments should be updated, and we want to make a patch request.
        interface Payload {
          email?: string;
          name?: string;
          password?: string;
        }

        const payload: Payload = {};

        // Check which fields should be updated
        if (email !== user.value.email)
          payload['email'] = email;

        if (name !== user.value.name)
          payload['name'] = name;

        if (password)
          payload['password'] = password;

        // If there is data in the payload == if the button
        // was not pressed with no new data.
        if (Object.keys(payload).length > 0) {
          loading.value = true;
          try {
            await axios.patch(
              url,
              payload,
              authHeaders
            ).then(async () => {
              await getUserInfo();
              isSuccessful.value = true;
            });

          } catch (e) {
            console.error(e);
            // @ts-ignore
            errorMessage.value = e.message;
          } finally {
            loading.value = false;
          }
        }
      }
    }

    return {
      user,
      token,
      errorMessage,
      loading,
      isSuccessful,
      handleRegister,
      handleLogin,
      getUserInfo,
      updateUserProfile,
    }
  }
)
