import Vue from 'vue'

export default class CookieHandler extends Vue {
  /**
   * Set a cookie with the specified name, value, and expiration time
   * @param name - the name of the cookie
   * @param value - the value to be stored in the cookie
   * @param expiration - the expiration time of the cookie in days (default: 30 days)
   */
  public static setCookie(name: string, value: string, expiration: number = 30) {
    const date = new Date()
    date.setTime(date.getTime() + expiration * 24 * 60 * 60 * 1000)
    const expires = "; expires=" + date.toUTCString()
    document.cookie = name + "=" + value + expires + "; path=/"
  }

  /**
   * Get the value of a cookie with the specified name
   * @param name - the name of the cookie to get
   * @returns the value of the cookie, or null if the cookie does not exist
   */
  public static getCookie(name: string): string | null {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.startsWith(name + "=")) {
        return cookie.substring(name.length + 1, cookie.length)
      }
    }
    return null
  }

  /**
   * Delete a cookie with the specified name
   * @param name - the name of the cookie to delete
   */
  public static deleteCookie(name: string) {
    CookieHandler.setCookie(name, "", -1)
  }
}

