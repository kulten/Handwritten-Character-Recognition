const {app,dialog, BrowserWindow, ipcMain} = require('electron')
const cp = require('child_process')
let win

app.on('ready', ()=>{
  win = new BrowserWindow({width: 800, height:600})
  win.loadFile('./public/html/index.html')
})
app.on('closed', ()=>{
  win = null
})
app.on('window-all-closed',()=>{
  app.quit()
})
ipcMain.on('asynchronous-message', (event, arg) => {
  const ls = cp.spawn('python', ['textprep.py', arg]);
  var s
  ls.stdout.on('data', (data) => {
    console.log(`${data}`)
    event.sender.send('asynchronous-reply',`${data}`)
  });

  ls.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
  });

  ls.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
})
