export const requestNotificationPermission = async () => {
  if (!('Notification' in window)) {
    return 'unsupported'
  }

  const permission = await Notification.requestPermission()

  if (permission === 'granted') {
    localStorage.setItem('uv_notifications_enabled', 'true')
  } else {
    localStorage.setItem('uv_notifications_enabled', 'false')
  }

  return permission
}

export const areNotificationsEnabled = () => {
  return localStorage.getItem('uv_notifications_enabled') === 'true'
}

export const disableNotifications = () => {
  localStorage.setItem('uv_notifications_enabled', 'false')
}

export const notifyHighUV = (uvValue) => {
  if (!('Notification' in window)) return
  if (Notification.permission !== 'granted') return
  if (!areNotificationsEnabled()) return
  if (uvValue < 6) return

  const notification = new Notification('High UV Alert', {
    body: `Current UV is ${uvValue}. Seek shade and apply sunscreen. (${new Date().toLocaleTimeString()})`,
    tag: `uv-alert-${Date.now()}`,
    requireInteraction: true,
  })

}