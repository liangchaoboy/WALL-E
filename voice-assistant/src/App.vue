<template>
  <div class="container">
    <div class="permission-prompt" v-if="!permissionGranted">
      <h2>麦克风权限请求</h2>
      <p>小度语音助手需要访问您的麦克风才能工作。</p>
      <p>请点击"允许"以启用语音识别功能。</p>
      <button class="permission-btn" @click="requestMicrophonePermission">启用麦克风</button>
      <p class="debug-info" style="margin-top: 20px; max-width: 500px;">
        如果麦克风权限被拒绝，请检查浏览器地址栏旁边的麦克风图标，并确保已允许此网站使用麦克风。
      </p>
    </div>

    <div class="assistant" :class="{ active: isListening }">
      <div class="assistant-icon">🐾</div>
      <div class="sound-wave">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>
    </div>

    <div class="status">{{ statusText }}</div>
    <button 
      class="btn" 
      :class="{ listening: isListening }"
      @click="toggleListening"
    >
      {{ isListening ? '停止聆听' : '开始聆听' }}
    </button>
    <div class="response" :class="{ show: responseText }">
      {{ responseText }}
    </div>

    <div class="debug-info">
      <!-- <div>调试信息:</div> -->
      <div class="debug-log" ref="debugLog">
        <div v-for="(log, index) in debugLogs" :key="index">{{ log }}</div>
      </div>
    </div>

    <div class="particles">
      <div 
        class="particle" 
        v-for="(particle, index) in particles" 
        :key="index"
        :style="particle.style"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isListening: false,
      permissionGranted: false,
      statusText: '点击按钮开始语音唤醒',
      responseText: '',
      debugLogs: [
        // '[19:34:58] 浏览器支持语音识别API',
        // '[19:34:58] 麦克风权限已授予',
        '[19:35:03] 开始语音识别',
        //'[19:35:03] 语音识别已启动'
      ],
      recognition: null,
      particles: Array.from({ length: 30 }, () => ({
        style: {
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 5}s`,
          width: `${3 + Math.random() * 4}px`,
          height: `${3 + Math.random() * 4}px`
        }
      })),
      // 新增：保存最后一次完整语音转录
      lastTranscript: ''
    }
  },
  methods: {
    addDebugLog(message) {
      const timestamp = new Date().toLocaleTimeString()
      this.debugLogs.push(`[${timestamp}] ${message}`)
      if (this.debugLogs.length > 20) this.debugLogs.shift()
      this.$nextTick(() => {
        // 修改后代码
      if (this.$refs.debugLog) {
        this.$refs.debugLog.scrollTop = this.$refs.debugLog.scrollHeight
      }
      })
    },
    checkBrowserSupport() {
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        this.statusText = '您的浏览器不支持语音识别，请使用Chrome或Edge。'
        return false
      }
      return true
    },
    initSpeechRecognition() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      this.recognition = new SpeechRecognition()
      
      this.recognition.lang = 'zh-CN'
      this.recognition.continuous = true
      this.recognition.interimResults = false
      
      // 修改事件处理程序
      this.recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript
        if (transcript != ""){
           this.addDebugLog(`主人: "${transcript}"`)
        
        //if (transcript.toLowerCase().includes('你好')) {
          this.statusText = '唤醒词已识别'
          this.sendToNavigationServer(transcript)
          
          const responses = ['我在', '哎，我在呢', '有什么可以帮您?', '请说']
          this.responseText = responses[Math.floor(Math.random() * responses.length)]
          
          setTimeout(() => {
            this.responseText = ''
            this.statusText = '正在聆听...'
          }, 3000)
        }
        //}
      }
      
      // 新增：在语音识别结束时触发请求
      this.recognition.onend = () => {
        this.addDebugLog('语音识别结束')
        // 只有在识别过程中有结果时才发送请求
        if (this.isListening) {
          this.sendToNavigationServer('语音识别结束')
        }
        
        if (this.isListening) this.recognition.start()
      }

      this.recognition.onerror = (event) => {
        if (event.error === 'not-allowed') {
          this.statusText = '麦克风权限被拒绝'
          this.permissionGranted = false
          this.stopListening()
        } else {
          this.statusText = '识别错误: ' + event.error
        }
      }
      
      this.recognition.onstart = () => {
        this.statusText = '正在聆听...请说"小悦小悦"'
      }
      
      this.recognition.onend = () => {
        if (this.isListening) this.recognition.start()
      }
    },
    async requestMicrophonePermission() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        stream.getTracks().forEach(track => track.stop())
        this.permissionGranted = true
        this.initSpeechRecognition()
      } catch (error) {
        this.statusText = '麦克风权限被拒绝'
      }
    },
    toggleListening() {
      if (!this.permissionGranted) {
        this.requestMicrophonePermission()
        return
      }
      
      if (this.isListening) {
        this.stopListening()
      } else {
        this.startListening()
      }
    },
    startListening() {
      if (!this.recognition) return
      try {
        this.recognition.start()
        this.isListening = true
      } catch (error) {
        this.statusText = '启动失败，请重试'
      }
    },
    // 修改停止监听方法
    async stopListening() {
      if (this.recognition) {
        this.recognition.stop()
      }
      this.isListening = false
      this.statusText = '点击按钮开始语音唤醒'
    },
    
    async sendToNavigationServer(text) {
      try {
        //this.addDebugLog(`向服务端请求导航：语音内容="${text}"`)
        const encodedText = encodeURIComponent(text)
        const response = await fetch(`http://localhost:9004/get-text?text=${encodedText}`)
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || `服务端错误：${response.status}`)
        }
        
        const data = await response.json()
        // 将完整服务端响应输出到调试台
        this.addDebugLog(`小度小度：${data.data}`)
        
        // 只有URL不为空时才跳转
        if (data.url && data.url.trim() !== '') {
          //this.addDebugLog(`服务端返回导航URL：${data.url}`)
          window.open(data.url, '_blank')
          this.statusText = '正在打开导航页面...'
        } else {
          //this.addDebugLog('服务端返回的URL为空，不进行跳转')
          this.statusText = '未获取到导航链接'
        }
        
        setTimeout(() => {
          this.statusText = '正在聆听...'
        }, 3000)
        
      } catch (error) {
        this.addDebugLog(`导航请求失败：${error.message}`)
        this.statusText = '导航失败，请重试'
      }
    }
  },
  mounted() {
    if (this.checkBrowserSupport()) {
      this.requestMicrophonePermission()
    }
  }
}
</script>

<style>
/* 保持原有样式不变 */
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Arial', sans-serif;
  color: white;
  overflow: hidden;
}

.container {
  position: relative;
  width: 90%;
  max-width: 500px;
  text-align: center;
  z-index: 10;
}

.assistant {
  width: 200px;
  height: 200px;
  margin: 0 auto 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  box-shadow: 0 0 30px rgba(0, 150, 255, 0.3);
  transition: all 0.3s ease;
}

.assistant.active {
  background: rgba(0, 150, 255, 0.2);
  box-shadow: 0 0 50px rgba(0, 150, 255, 0.5);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 30px rgba(0, 150, 255, 0.3);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 50px rgba(0, 150, 255, 0.7);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 30px rgba(0, 150, 255, 0.3);
  }
}

.assistant-icon {
  font-size: 60px;
  color: #0096ff;
  transition: all 0.3s ease;
}

.assistant.active .assistant-icon {
  color: #00d4ff;
}

.status {
  margin-bottom: 20px;
  font-size: 18px;
  height: 24px;
  transition: all 0.3s ease;
}

.btn {
  background: linear-gradient(45deg, #0096ff, #00d4ff);
  border: none;
  color: white;
  padding: 12px 30px;
  border-radius: 50px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
  box-shadow: 0 5px 15px rgba(0, 150, 255, 0.4);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: all 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 150, 255, 0.6);
}

.btn:active {
  transform: translateY(0);
}

.btn.listening {
  background: linear-gradient(45deg, #ff416c, #ff4b2b);
  animation: pulse 1.5s infinite;
}

.response {
  margin-top: 30px;
  font-size: 24px;
  min-height: 36px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease;
}

.response.show {
  opacity: 1;
  transform: translateY(0);
}

.sound-wave {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.assistant.active .sound-wave {
  opacity: 1;
}

.bar {
  width: 4px;
  height: 10px;
  background: #0096ff;
  border-radius: 2px;
  animation: soundWave 1.5s infinite ease-in-out;
  opacity: 0;
}

.bar:nth-child(1) { animation-delay: 0.1s; }
.bar:nth-child(2) { animation-delay: 0.2s; }
.bar:nth-child(3) { animation-delay: 0.3s; }
.bar:nth-child(4) { animation-delay: 0.4s; }
.bar:nth-child(5) { animation-delay: 0.5s; }

@keyframes soundWave {
  0%, 100% {
    height: 10px;
    opacity: 0.3;
  }
  50% {
    height: 50px;
    opacity: 1;
  }
}

.debug-info {
  position: relative;
  margin-top: 20px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  text-align: left;
  background: rgba(0, 0, 0, 0.3);
  padding: 10px;
  border-radius: 5px;
  max-height: 250px;
  overflow-y: auto;
  width: 150%;
  border: 1px solid rgba(255, 0, 0, 0.3);
  left: -40px;
   /* 新增：控制文本换行 */
  white-space: pre-wrap;  /* 保留空格，同时自动换行 */
  word-break: break-word; /* 强制长文本/单词换行 */
}

.debug-log {
  width: 100%; /* 宽度自适应父容器 */
  max-height: 100px;
  overflow-y: auto;
  margin-top: 5px;
  font-family: 'Courier New', monospace;
}

.debug-log div {
  padding: 2px 0;
  line-height: 1.4;
}

.permission-prompt {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  flex-direction: column;
  padding: 20px;
  text-align: center;
}

.permission-btn {
  margin-top: 20px;
  background: #0096ff;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.particle {
  position: absolute;
  background: rgba(0, 150, 255, 0.6);
  border-radius: 50%;
  animation: float 5s infinite ease-in-out;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
}
</style>