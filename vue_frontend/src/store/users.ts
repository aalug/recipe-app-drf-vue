import {ref} from 'vue';
import {defineStore} from 'pinia';
import axios from 'axios';
import {User} from '@/types/User';
import {validateEmail} from '@/utils/validate-email';

export const useUserStore = defineStore('users', () => {
  const user = ref<User | null>(null);
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

  return {
    user,
    errorMessage,
    loading,
    isSuccessful,
    handleRegister,
    handleLogin,
  }
})
