/**
 * Copyright (c) 2011-2017 Berkeley Model United Nations. All rights reserved.
 * Use of this source code is governed by a BSD License (see LICENSE).
 */

'use strict';

var Button = require('components/core/Button');
var NumberInput = require('components/NumberInput');

var cx = require('classnames');
var React = require('react');

var PaperSubmissionTable = React.createClass({
  propTypes: {
    onUpload: React.PropTypes.func,
    onSubmit: React.PropTypes.func,
    rubric: React.PropTypes.object,
    paper: React.PropTypes.object,
    files: React.PropTypes.object,
  },

  render() {
    var rubric = this.props.rubric;
    var paper = this.props.paper;
    var files = this.props.files;
    var buttons = <div>Waiting on server...</div>;

    if (paper.id in files) {
      var url = window.URL;
      var hrefData = url.createObjectURL(files[paper.id]);
      var fileNames = paper.file.split('/');
      var fileName = fileNames[fileNames.length - 1];
      buttons = (
        <div>
          <a
            className={cx({
              button: true,
              'button-large': true,
              'button-green': true,
              'rounded-small': true,
            })}
            href={hrefData}
            download={fileName}>
            Download Paper
          </a>
        </div>
      );
    }

    if (!paper.graded) {
      return (
        <div>
          <table>
            <tbody>
              <tr>
                <td>Upload Paper:</td>
                <td>
                  <div>
                    <input
                      type="file"
                      accept=".doc, .docx, .pdf, application/pdf, application/ms-word, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                      onChange={this._handleUpload}
                    />
                    <input type="submit" onClick={this._handleSubmit} />
                  </div>
                </td>
              </tr>
              <tr>
                <td>Download Paper:</td>
                <td>{buttons}</td>
              </tr>
            </tbody>
          </table>
        </div>
      );
    }

    return (
      <div>
        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th>Score</th>
              <th>Max Score</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{rubric.grade_category_1}</td>
              <td>
                <NumberInput defaultValue={'' + paper.score_1} disabled />
              </td>
              <td>{rubric.grade_value_1}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_2}</td>
              <td>
                <NumberInput defaultValue={'' + paper.score_2} disabled />
              </td>
              <td>{rubric.grade_value_2}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_3}</td>
              <td>
                <NumberInput defaultValue={'' + paper.score_3} disabled />
              </td>
              <td>{rubric.grade_value_3}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_4}</td>
              <td>
                <NumberInput defaultValue={'' + paper.score_4} disabled />
              </td>
              <td>{rubric.grade_value_4}</td>
            </tr>
            <tr>
              <td>{rubric.grade_category_5}</td>
              <td>
                <NumberInput defaultValue={'' + paper.score_5} disabled />
              </td>
              <td>{rubric.grade_value_5}</td>
            </tr>
          </tbody>
        </table>
        {buttons}
      </div>
    );
  },

  _handleUpload: function(event) {
    this.props.onUpload && this.props.onUpload(this.props.paper.id, event);
  },

  _handleSubmit: function(event) {
    this.props.onSubmit && this.props.onSubmit(this.props.paper.id, event);
  },
});

module.exports = PaperSubmissionTable;