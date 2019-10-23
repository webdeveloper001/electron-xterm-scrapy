// @flow
import React, { Component } from 'react';
import { remote, shell } from 'electron';
import { Terminal } from 'xterm';
import * as os from 'os';
import * as pty from 'node-pty';
import styles from './Home.css';

export default class Home extends Component {

  constructor(props) {
    super(props);

    this.state = {
      scrappers: [
        {
          name: 'BCPA',
          commands: [
            'cd BASE_PATH/scrappers/bcpa',
            'scrapy crawl bcpa_prop -a input_file=INPUT_FILE_PATH'
          ],
          input_file: '',
          output_folder: 'scrappers/bcpa'
        },
        {
          name: 'Miamidade',
          commands: [
            'cd BASE_PATH/scrappers/miamidade',
            'scrapy crawl miami_prop -a input_file=INPUT_FILE_PATH'
          ],
          input_file: '',
          output_folder: 'scrappers/miamidade'
        },
        {
          name: 'New BCPA',
          commands: [
            'cd BASE_PATH/scrappers/new_bcpa',
            'python bcpa.py INPUT_FILE_PATH'
          ],
          input_file: '',
          output_folder: 'scrappers/new_bcpa'
        },
        {
          name: 'PBC gov',
          commands: [
            'cd BASE_PATH/scrappers/pbcgov',
            'python pbcgov.py INPUT_FILE_PATH'
          ],
          input_file: '',
          output_folder: 'scrappers/pbcgov'
        }
      ]
    }

    this.terminals = []
    this.base_path = remote.app.getPath('documents');
    console.log(this.base_path);
    this.state.scrappers.map(scrapper => {
      const term = new Terminal()
      const ptyProc = pty.spawn(os.platform() === 'win32' ? 'powershell.exe' : process.env.SHELL || '/bin/bash', [], {
        cols: term.cols,
        rows: term.rows
      });
      term.onData(data => {
        ptyProc.write(data);
      });
      ptyProc.on('data', data => {
        term.write(data);
      });
      ptyProc.write(`cd ${this.base_path}\n`);
      this.terminals.push({
        term,
        ptyProc
      });
    })
  }

  componentDidMount() {
    const { scrappers } = this.state;
    scrappers.map((scrapper, idx) => {
      this.terminals[idx].term.open(document.getElementById(scrapper.name))
    })
  }

  openDirectory(path) {
    shell.openItem(path);
  }

  parseCommands = (scrapper) => {
    let { base_path } = this;
    console.log(scrapper);
    return scrapper.commands.map((c => {
      c = c.replace('INPUT_FILE_PATH', scrapper.input_file);
      c = c.replace('BASE_PATH', base_path);
      return c;
    }));
  }

  runCommands(term, commands) {
    commands.map(c => {
      term.ptyProc.write(c);
      term.ptyProc.write("\n");
      term.term.scrollToBottom();
    })
  }

  render() {
    const { scrappers } = this.state;
    const { parseCommands } = this;

    return (
      <div className={styles.container} data-tid="container">
        <h2>Scrappers</h2>
        <div className="scrappers-wrapper">
          {scrappers.map((scrapper, idx) => {
            return (
              <div key={idx}>
                <h3>{scrapper.name}</h3>
                <div className="w-100 d-flex justify-content-between">
                  <div className="scrapper-input-box">
                    <label>{scrapper.input_file || 'Choose Input File'}</label>
                    <input type="file"
                      // accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                      onChange={ev => {
                        console.log(ev.target.files[0].path);
                        let path = ev.target.files[0].path;
                        scrappers[idx].input_file = path;
                        this.setState({
                          scrappers
                        })
                      }}
                    />
                  </div>
                  <div className="control-panel d-inline ml-auto">
                    <button className="btn btn-primary mr-2"
                      onClick={() => {
                        let commands = parseCommands(scrapper);
                        this.runCommands(this.terminals[idx], commands);
                      }}
                      disabled={scrapper.input_file === ""} >Run!</button>
                    <button className="btn btn-primary" onClick={() => {
                      this.openDirectory(scrapper.output_folder);
                    }}>Open Output folder</button>
                  </div>
                </div>
                <div className="scrapper-commands-preview mt-2 mb-3">
                  <span>Commands Preview</span>
                  {parseCommands(scrapper).map((c => {
                    c = c.replace('INPUT_FILE_PATH', scrapper.input_file);
                    return <pre className="mb-0" key={c}>{c}</pre>;
                  }))}
                </div>
                <div id={scrapper.name} className="terminal">
                </div>
              </div>
            )
          })}
        </div>
      </div>
    );
  }
}
