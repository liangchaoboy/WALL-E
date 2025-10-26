// swift-tools-version: 5.9

import PackageDescription

let package = Package(
    name: "WALLE",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(
            name: "WALLE",
            targets: ["WALLE"]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/grpc/grpc-swift.git", from: "1.20.0"),
        .package(url: "https://github.com/Picovoice/porcupine.git", from: "3.0.0"),
    ],
    targets: [
        .executableTarget(
            name: "WALLE",
            dependencies: [
                .product(name: "GRPC", package: "grpc-swift"),
                .product(name: "Porcupine-iOS", package: "porcupine"),
            ],
            path: "WALLE"
        )
    ]
)
