var concat = require('gulp-concat'),
    gulp = require('gulp'),
    gulpFilter = require('gulp-filter'),
    jshint = require('gulp-jshint'),
    mainBowerFiles = require('main-bower-files'),
    path = require('path');


// Directory where the results go
var output_directory = path.join('fetsy', 'static');

var specialJSFilter = function (exclude) {
    return function (file) {
        var name = path.basename(file);
        if (exclude) {
            return name !== 'html5shiv.js' && name !== 'respond.src.js' && path.extname(name) == '.js';
        } else {
            return name === 'html5shiv.js' || name == 'respond.src.js';
        }
    };
};


// Catches all JavaScript files from all bower components and concats them to
// one file js/fetsy-libs.js. HTML5 Shiv and Respond.js are excluded.
gulp.task('js', function() {
    return gulp.src(mainBowerFiles({filter: specialJSFilter(true)}))
        .pipe(concat('fetsy-libs.js'))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});


// Catches HTML5 Shiv and Respond.js and moves them to the output directory.
gulp.task('special-js', function () {
    return gulp.src(mainBowerFiles({filter: specialJSFilter(false)}))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});


// Catches all CSS files from all bower components and concats them to one file
// css/fetsy-libs.css.
gulp.task('css', function() {
    return gulp.src(mainBowerFiles({
        filter: /\.css$/
    }))
    .pipe(concat('fetsy-libs.css'))
    .pipe(gulp.dest(path.join(output_directory, 'css')));
});


// Catches all font files from all bower components.
gulp.task('fonts', function() {
    return gulp.src(mainBowerFiles({
        filter: /\.(eot)|(svg)|(ttf)|(woff)$/
    }))
    .pipe(gulp.dest(path.join(output_directory, 'fonts')));
});


// Checks JS using JSHint
gulp.task('jshint', function() {
  return gulp.src(['./gulpfile.js', './fetsy/static/js/*.js'])
    .pipe(gulpFilter(function (file) {
            return specialJSFilter(true)(file.path);
        }))
    .pipe(gulpFilter(['*', '!fetsy-libs.js', '!html5shiv.js', '!respond.src.js']))
    .pipe(jshint())
    .pipe(jshint.reporter('default'));
});


// Gulp default task
gulp.task('default', ['js', 'special-js', 'css', 'fonts'], function() {});
