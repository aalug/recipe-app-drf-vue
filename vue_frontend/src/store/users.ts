import {ref} from 'vue'
import {defineStore} from 'pinia'
import axios from 'axios'
import {User} from '@/types/User'
import {validateEmail} from '@/utils/validate-email'

export const useUserStore = defineStore('users', () => {
  const user = ref<User | null>(null)
  const errorMessage = ref<string>('')
  const loading = ref<boolean>(false)
  const isSuccessful = ref<boolean>(false)

  const handleRegister = async (email: string,
                                name: string,
                                password: string) => {

    if (!validateEmail(email)) {
      return errorMessage.value = 'E-mail is invalid'
    }

    if (!name) {
      return errorMessage.value = 'Name is required'
    }

    if (password.length < 6) {
      return errorMessage.value = 'Password must be at least 6 characters'
    }

    errorMessage.value = ''

    loading.value = true
    try {
      await axios.post(
        `${import.meta.env.VITE_API_BASE}/user/create/`,
        {
          email: email,
          password: password,
          name: name
        }
      )
      isSuccessful.value = true
    } catch (e) {
      // @ts-ignore
      if (e.response.status === 400) {
        // @ts-ignore
        const errorData = e.response.data
        const message = ref<string>('')
        if (errorData.email && errorData.name) {
          message.value = 'User with this email and name already exists'
        } else if (errorData.email) {
          message.value = errorData.email[0]
        } else if (errorData.name) {
          message.value = errorData.name[0]
        }
        errorMessage.value = message.value ? message.value : 'Error occurred while creating an account'
      } else {
        errorMessage.value = 'Error occurred while creating an account'
      }
    } finally {
      loading.value = false
    }
  }


  return {
    user,
    errorMessage,
    loading,
    isSuccessful,
    handleRegister,
  }
})
