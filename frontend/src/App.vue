<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>CRM管理系统</h1>
          <el-menu
            :default-active="$route.path"
            mode="horizontal"
            router
            class="nav-menu"
          >
            <el-menu-item index="/companies">
              <el-icon><Office /></el-icon>
              <span>公司管理</span>
            </el-menu-item>
            <el-menu-item index="/talents">
              <el-icon><User /></el-icon>
              <span>人才管理</span>
            </el-menu-item>
            <el-menu-item index="/communications">
              <el-icon><ChatDotRound /></el-icon>
              <span>沟通记录</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  background-color: #545c64;
  color: white;
  padding: 0;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.header-content h1 {
  margin: 0;
  margin-right: 50px;
  font-size: 24px;
}

.nav-menu {
  background-color: transparent;
  border-bottom: none;
}

.nav-menu .el-menu-item {
  color: white;
}

.nav-menu .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-menu .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
  border-bottom: 2px solid #409eff;
}

.el-main {
  padding: 20px;
}
</style>
