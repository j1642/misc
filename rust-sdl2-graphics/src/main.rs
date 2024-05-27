extern crate sdl2;

use sdl2::event::Event;
use sdl2::keyboard::Keycode;
use sdl2::pixels::Color;
use std::time::Duration;

const WINDOW_WIDTH: i32 = 800;
const WINDOW_HEIGHT: i32 = 500;

// https://rust-sdl2.github.io/rust-sdl2/sdl2/render/struct.Canvas.html

pub fn main() {
    let sdl_context = sdl2::init().unwrap();
    let video_subsystem = sdl_context.video().unwrap();

    let window = video_subsystem
        .window("rust-sdl2 demo", WINDOW_WIDTH as u32, WINDOW_HEIGHT as u32)
        .position_centered()
        .build()
        .unwrap();

    let mut canvas = window.into_canvas().build().unwrap();

    canvas.set_draw_color(Color::RGB(0, 255, 255));
    canvas.clear();
    canvas.present();

    // in the window, (0px, 0px) is the top left corner
    let triangles: [[Point3d; 3]; 12] = [
        // South face
        [
            Point3d {
                x: 0.,
                y: 0.,
                z: 0.,
            },
            Point3d {
                x: 0.,
                y: 1.,
                z: 0.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 0.,
            },
        ],
        [
            Point3d {
                x: 0.,
                y: 0.,
                z: 0.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 0.,
            },
            Point3d {
                x: 1.,
                y: 0.,
                z: 0.,
            },
        ],
        // North
        [
            Point3d {
                x: 1.,
                y: 0.,
                z: 1.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 1.,
            },
            Point3d {
                x: 0.,
                y: 1.,
                z: 1.,
            },
        ],
        [
            Point3d {
                x: 1.,
                y: 0.,
                z: 1.,
            },
            Point3d {
                x: 0.,
                y: 1.,
                z: 1.,
            },
            Point3d {
                x: 0.,
                y: 0.,
                z: 1.,
            },
        ],
        // East
        [
            Point3d {
                x: 1.,
                y: 0.,
                z: 0.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 0.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 1.,
            },
        ],
        [
            Point3d {
                x: 1.,
                y: 0.,
                z: 0.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 1.,
            },
            Point3d {
                x: 1.,
                y: 0.,
                z: 1.,
            },
        ],
        // West
        [
            Point3d {
                x: 0.,
                y: 0.,
                z: 1.,
            },
            Point3d {
                x: 0.,
                y: 1.,
                z: 1.,
            },
            Point3d {
                x: 0.,
                y: 1.,
                z: 0.,
            },
        ],
        [
            Point3d {
                x: 0.,
                y: 0.,
                z: 1.,
            },
            Point3d {
                x: 0.,
                y: 1.,
                z: 0.,
            },
            Point3d {
                x: 0.,
                y: 0.,
                z: 0.,
            },
        ],
        // Top
        [
            Point3d {
                x: 0.,
                y: 1.,
                z: 0.,
            },
            Point3d {
                x: 0.,
                y: 1.,
                z: 1.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 1.,
            },
        ],
        [
            Point3d {
                x: 0.,
                y: 1.,
                z: 0.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 1.,
            },
            Point3d {
                x: 1.,
                y: 1.,
                z: 0.,
            },
        ],
        // Bottom
        [
            Point3d {
                x: 1.,
                y: 0.,
                z: 0.,
            },
            Point3d {
                x: 1.,
                y: 0.,
                z: 1.,
            },
            Point3d {
                x: 0.,
                y: 0.,
                z: 1.,
            },
        ],
        [
            Point3d {
                x: 1.,
                y: 0.,
                z: 0.,
            },
            Point3d {
                x: 0.,
                y: 0.,
                z: 1.,
            },
            Point3d {
                x: 0.,
                y: 0.,
                z: 0.,
            },
        ],
    ];

    // Projection matrix
    let f_near = 0.1;
    let f_far = 1000.0;
    let f_fov = 90.0; // field of view
    let f_aspect_ratio = WINDOW_HEIGHT as f64 / WINDOW_WIDTH as f64;
    let f_fov_rad = 1.0 / (f_fov * 0.5f64).tan();

    let mut matrix: [[f64; 4]; 4] = [[0.0; 4]; 4];
    matrix[0][0] = f_aspect_ratio * f_fov_rad;
    matrix[1][1] = f_fov_rad;
    matrix[2][2] = f_far / (f_far - f_near);
    matrix[3][2] = (-f_far * f_near) / (f_far - f_near);
    matrix[2][3] = 1.0;
    matrix[3][3] = 0.0;

    let start = std::time::Instant::now();
    let mut event_pump = sdl_context.event_pump().unwrap();
    'running: loop {
        canvas.set_draw_color(Color::RGB(0, 64, 255));
        canvas.clear();
        for event in event_pump.poll_iter() {
            match event {
                Event::Quit { .. }
                | Event::KeyDown {
                    keycode: Some(Keycode::Escape),
                    ..
                } => break 'running,
                _ => {}
            }
        }

        canvas.set_draw_color(Color::BLACK);
        // "coercing an array to a slice" from rust docs
        //let points: &[sdl2::rect::Point] = &[front_botl, front_botr, front_topr, front_topl];

        // Rotation matrices
        let elapsed = start.elapsed().as_secs_f64();
        let f_theta = 1. * elapsed;

        let mut z_rot: [[f64; 4]; 4] = [[0.; 4]; 4];
        z_rot[0][0] = f_theta.cos();
        z_rot[0][1] = f_theta.sin();
        z_rot[1][0] = -f_theta.sin();
        z_rot[1][1] = f_theta.cos();
        z_rot[2][2] = 1.;
        z_rot[3][3] = 1.;

        let mut x_rot: [[f64; 4]; 4] = [[0.; 4]; 4];
        x_rot[0][0] = 1.;
        x_rot[1][1] = (f_theta * 0.5).cos();
        x_rot[1][2] = (f_theta * 0.5).sin();
        x_rot[2][1] = -1. * (f_theta * 0.5).sin();
        x_rot[2][2] = (f_theta * 0.5).cos();
        x_rot[3][3] = 1.;

        for i in 0..triangles.len() {
            let mut z_rot_tri: [Point3d; 3] = triangles[i];
            multiply_matrix_vector(z_rot, triangles[i][0], &mut z_rot_tri[0]);
            multiply_matrix_vector(z_rot, triangles[i][1], &mut z_rot_tri[1]);
            multiply_matrix_vector(z_rot, triangles[i][2], &mut z_rot_tri[2]);

            let mut xz_rot_tri: [Point3d; 3] = triangles[i];
            multiply_matrix_vector(x_rot, z_rot_tri[0], &mut xz_rot_tri[0]);
            multiply_matrix_vector(x_rot, z_rot_tri[1], &mut xz_rot_tri[1]);
            multiply_matrix_vector(x_rot, z_rot_tri[2], &mut xz_rot_tri[2]);

            // add space between camera and viewed object
            let mut translated_tri = xz_rot_tri;
            // Error from convert_coord_to_pixels() with translations of 1., 2.
            translated_tri[0].z = xz_rot_tri[0].z + 3.;
            translated_tri[1].z = xz_rot_tri[1].z + 3.;
            translated_tri[2].z = xz_rot_tri[2].z + 3.;

            let mut projected_tri: [Point3d; 3] = [Point3d {
                x: 0.,
                y: 0.,
                z: 0.,
            }; 3];
            multiply_matrix_vector(matrix, translated_tri[0], &mut projected_tri[0]);
            multiply_matrix_vector(matrix, translated_tri[1], &mut projected_tri[1]);
            multiply_matrix_vector(matrix, translated_tri[2], &mut projected_tri[2]);
            draw_triangle(projected_tri, &mut canvas);
        }

        canvas.present();
        std::thread::sleep(Duration::from_millis(10));
    }
    // Test x conversions
    assert_eq!(
        convert_coord_to_pixels(-1.0, 1.0).unwrap(),
        sdl2::rect::Point::new(0, 0)
    );
    assert_eq!(
        convert_coord_to_pixels(0.0, 1.0).unwrap(),
        sdl2::rect::Point::new(WINDOW_WIDTH as i32 / 2, 0)
    );
    assert_eq!(
        convert_coord_to_pixels(1.0, 1.0).unwrap(),
        sdl2::rect::Point::new(WINDOW_WIDTH as i32, 0)
    );
    // Test y conversions
    assert_eq!(
        convert_coord_to_pixels(-1.0, -1.0).unwrap(),
        sdl2::rect::Point::new(0, WINDOW_HEIGHT as i32)
    );
    assert_eq!(
        convert_coord_to_pixels(-1.0, 0.0).unwrap(),
        sdl2::rect::Point::new(0, WINDOW_HEIGHT as i32 / 2)
    );
    assert_eq!(
        convert_coord_to_pixels(-1.0, 1.0).unwrap(),
        sdl2::rect::Point::new(0, 0)
    );
}

fn convert_coord_to_pixels(x: f64, y: f64) -> Result<sdl2::rect::Point, &'static str> {
    // 0,0 to half width, half height
    // -1,-1 to 0, max height
    // 1,1 to max width, 0
    if x < -1.0 || 1.0 < x || y < -1.0 || 1.0 < y {
        return Err("x and y must be in range [-1.0, 1.0]");
    }
    let x_pixel: i32 = (x * (WINDOW_WIDTH / 2) as f64) as i32 + WINDOW_WIDTH / 2;
    let y_pixel: i32 = (-1.0 * y * (WINDOW_HEIGHT / 2) as f64) as i32 + WINDOW_HEIGHT / 2;

    return Ok(sdl2::rect::Point::new(x_pixel, y_pixel));
}

#[derive(Copy, Clone, Debug)]
struct Point3d {
    x: f64,
    y: f64,
    z: f64,
}

fn multiply_matrix_vector(matrix: [[f64; 4]; 4], vec_in: Point3d, vec_out: &mut Point3d) {
    vec_out.x =
        vec_in.x * matrix[0][0] + vec_in.y * matrix[1][0] + vec_in.z * matrix[2][0] + matrix[3][0];
    vec_out.y =
        vec_in.x * matrix[0][1] + vec_in.y * matrix[1][1] + vec_in.z * matrix[2][1] + matrix[3][1];
    vec_out.z =
        vec_in.x * matrix[0][2] + vec_in.y * matrix[1][2] + vec_in.z * matrix[2][2] + matrix[3][2];

    let w: f64 =
        vec_in.x * matrix[0][3] + vec_in.y * matrix[1][3] + vec_in.z * matrix[2][3] + matrix[3][3];
    // divide by w to get from 4d space to 3d space
    if w != 0.0 {
        vec_out.x /= w;
        vec_out.y /= w;
        vec_out.z /= w;
    }
}

fn draw_triangle(triangle: [Point3d; 3], canvas: &mut sdl2::render::WindowCanvas) {
    let mut points: [sdl2::rect::Point; 3] = [sdl2::rect::Point::new(0, 0); 3];
    for i in 0..triangle.len() {
        points[i] = convert_coord_to_pixels(triangle[i].x, triangle[i].y).unwrap();
    }

    for i in 0..points.len() - 1 {
        let res = canvas.draw_line(points[i], points[i + 1]);
        match res {
            Err(e) => {
                println!("error: {e:?}")
            }
            _ => {}
        }
    }
    let res = canvas.draw_line(points[points.len() - 1], points[0]);
    match res {
        Err(e) => {
            println!("error: {e:?}")
        }
        _ => {}
    }
}
