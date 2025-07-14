const net = require('net');
const fs = require('fs');
const path = require('path');

function checkPort(host, port, timeout = 400) {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    let status = null;

    socket.setTimeout(timeout);

    socket.on('connect', () => {
      status = 'open';
      socket.destroy();
    });

    socket.on('timeout', () => {
      status = 'closed';
      socket.destroy();
    });

    socket.on('error', () => {
      status = 'closed';
    });

    socket.on('close', () => {
      resolve({ port, status });
    });

    socket.connect(port, host);
  });
}

function parsePorts(portInput) {
  portInput = portInput.trim();
  if (portInput.includes(',')) {
    // List of ports: "80,443,8080"
    return portInput.split(',').map(p => parseInt(p.trim(), 10)).filter(p => p > 0 && p < 65536);
  } else if (portInput.includes('-')) {
    // Range: "20-25"
    const [start, end] = portInput.split('-').map(x => parseInt(x.trim(), 10));
    if (start > 0 && end > 0 && end >= start) {
      const ports = [];
      for (let p = start; p <= end; p++) ports.push(p);
      return ports;
    }
  } else {
    const p = parseInt(portInput, 10);
    if (p > 0 && p < 65536) return [p];
  }
  return [];
}

async function scanPorts(host, ports, concurrency = 50) {
  const results = [];
  let activeCount = 0;
  let index = 0;

  return new Promise((resolve) => {
    function next() {
      if (index >= ports.length && activeCount === 0) {
        resolve(results);
        return;
      }
      while (activeCount < concurrency && index < ports.length) {
        const port = ports[index++];
        activeCount++;
        checkPort(host, port).then((res) => {
          results.push(res);
          activeCount--;
          next();
        });
      }
    }
    next();
  });
}

function exportJSON(results, filename) {
  fs.writeFileSync(filename, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`Results saved to ${filename}`);
}

function exportCSV(results, filename) {
  const header = 'port,status\n';
  const rows = results.map(r => `${r.port},${r.status}`).join('\n');
  fs.writeFileSync(filename, header + rows, 'utf-8');
  console.log(`Results saved to ${filename}`);
}

function printHelp() {
  console.log(`
Usage:
  node port-scanner.js <host> -p <ports> [-o <outputfile>]

Options:
  <host>           Target IP or hostname to scan
  -p, --ports      Comma separated ports (e.g. 80,443) or range (e.g. 20-25)
  -o, --output     Optional output file (.json or .csv)
  -h, --help       Show this help message

Example:
  node port-scanner.js 192.168.1.1 -p 20-25,80,443 -o results.json
  node port-scanner.js example.com -p 80,443
`);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
    printHelp();
    process.exit(0);
  }

  const host = args[0];
  let portsArg = null;
  let outputFile = null;

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '-p' || args[i] === '--ports') {
      portsArg = args[i + 1];
      i++;
    } else if (args[i] === '-o' || args[i] === '--output') {
      outputFile = args[i + 1];
      i++;
    }
  }

  if (!portsArg) {
    console.error('Error: You must specify ports with -p');
    printHelp();
    process.exit(1);
  }

  const ports = [];

  portsArg.split(',').forEach(part => {
    part = part.trim();
    if (part.includes('-')) {
      const [start, end] = part.split('-').map(x => parseInt(x, 10));
      for (let p = start; p <= end; p++) {
        if (p > 0 && p < 65536) ports.push(p);
      }
    } else {
      const p = parseInt(part, 10);
      if (p > 0 && p < 65536) ports.push(p);
    }
  });

  if (ports.length === 0) {
    console.error('Error: No valid ports found');
    process.exit(1);
  }

  console.log(`Scanning ${host} on ports: ${ports.join(', ')}`);

  const results = await scanPorts(host, ports);

  results.forEach(({ port, status }) => {
    console.log(`Port ${port}: ${status}`);
  });

  if (outputFile) {
    const ext = path.extname(outputFile).toLowerCase();
    if (ext === '.json') {
      exportJSON(results, outputFile);
    } else if (ext === '.csv') {
      exportCSV(results, outputFile);
    } else {
      console.warn('Warning: Unsupported output format. Use .json or .csv');
    }
  }
}

main()