const net = require('net');
const fs = require('fs');

function parsePorts(portArg) {
  if (portArg.includes('-')) {
    const [start, end] = portArg.split('-').map(Number);
    if (isNaN(start) || isNaN(end) || start > end) {
      throw new Error('Invalid port range');
    }
    const ports = [];
    for (let p = start; p <= end; p++) {
      ports.push(p);
    }
    return ports;
  } else {
    return portArg.split(',').map(p => {
      const port = Number(p.trim());
      if (isNaN(port)) {
        throw new Error('Invalid port list');
      }
      return port;
    });
  }
}

function scanPort(host, port, timeout = 1000) {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    let status = 'closed';

    socket.setTimeout(timeout);

    socket.on('connect', () => {
      status = 'open';
      socket.destroy();
    });

    socket.on('timeout', () => {
      socket.destroy();
    });

    socket.on('error', () => {
    });

    socket.on('close', () => {
      resolve({ port, status });
    });

    socket.connect(port, host);
  });
}

function outputResults(results, format) {
  if (format === 'json') {
    const json = JSON.stringify(results, null, 2);
    fs.writeFileSync('scan_results.json', json);
    console.log('Results saved to scan_results.json');
  } else if (format === 'csv') {
    const header = 'port,status\n';
    const rows = results.map(r => `${r.port},${r.status}`).join('\n');
    fs.writeFileSync('scan_results.csv', header + rows);
    console.log('Results saved to scan_results.csv');
  } else {
    results.forEach(r => {
      console.log(`Port ${r.port}: ${r.status}`);
    });
  }
}

async function main() {
  const [,, host, portsArg, format] = process.argv;

  if (!host || !portsArg) {
    console.error('Usage: node portscanner.js <host> <port(s)> [json|csv]');
    console.error('Ports can be a range (20-80) or comma separated (22,80,443)');
    process.exit(1);
  }

  let ports;
  try {
    ports = parsePorts(portsArg);
  } catch (err) {
    console.error('Error parsing ports:', err.message);
    process.exit(1);
  }

  console.log(`Scanning ${host} on ports: ${ports.join(', ')}`);

  const results = [];
  for (const port of ports) {
    const res = await scanPort(host, port);
    results.push(res);
  }

  outputResults(results, format);
}

main();
